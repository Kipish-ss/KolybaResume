using System.Net;
using System.Net.Http.Json;
using AutoMapper;
using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.BLL.Services.Utility;
using KolybaResume.Common.Enums;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;
using KolybaResume.DTO;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.BLL.Services;

public class DouVacancyAggregatorService(KolybaResumeContext context, IMapper mapper, IEmailService emailService, IMachineLearningApiService apiService) : BaseService(context, mapper), IDouVacancyAggregatorService
{
    public async Task Aggregate()
    {
        var isFirstRun = !_context.Vacancies.Any();
        var companyLinks = await _context.Companies.Select(c => c.Url).Take(1500).ToListAsync();
        var addedVacancies = new List<Vacancy>();
        var allVacanciesIds = new List<int>();

        try
        {
            foreach (var link in companyLinks)
            {
                var vacancies = await GetVacancies($"{link}vacancies/export/", isFirstRun, allVacanciesIds);
                await _context.Vacancies.AddRangeAsync(vacancies);
                await _context.SaveChangesAsync();
                addedVacancies.AddRange(vacancies);
            }
        }
        finally
        {
            var vacanciesToDelete = (await _context.Vacancies.ToListAsync())
                .Where(v => v.Source == VacancySource.Dou &&
                            !allVacanciesIds.Contains(DouVacancyIdExtractor.GetId(v.Url)));
            
            _context.Vacancies.RemoveRange(vacanciesToDelete);
            await _context.SaveChangesAsync();

            var scores = new List<VacancyScoreResponse>();

            foreach (var batch in addedVacancies.Chunk(96))
            {
                scores.AddRange(await apiService.NotifyVacanciesUpdated(batch.Select(v => v.Id).ToArray()));
            }

            foreach (var userScore in scores.GroupBy(s => s.UserId))
            {
                var user = await _context.Users.FirstOrDefaultAsync(u => u.Id == userScore.Key);

                var relevantVacancies = userScore
                    .Where(us => us.Score > 60)
                    .Select(us => addedVacancies.First(v => v.Id == us.VacancyId)).ToArray();

                if (relevantVacancies.Any())
                {
                    await emailService.SendAsync(
                        user.Email,
                        user.Name,
                        "New relevant vacancies",
                        string.Join(Environment.NewLine, relevantVacancies.Select(v => $"{v.Title}: {v.Url}")));
                }
            }
        }
    }

    private async Task<Vacancy[]> GetVacancies(string url, bool isFirstRun, List<int> allVacanciesIds)
    {
        var handler = new HttpClientHandler
        {
            UseCookies = true,
            CookieContainer = new CookieContainer(),
            AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate
        };

        using var client = new HttpClient(handler);

        client.DefaultRequestHeaders.UserAgent.ParseAdd(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) " +
            "Chrome/114.0.0.0 Safari/537.36"
        );

        client.DefaultRequestHeaders.Accept.ParseAdd("application/json, text/javascript, */*; q=0.01");
        client.DefaultRequestHeaders.TryAddWithoutValidation("X-Requested-With", "XMLHttpRequest");

        using var request = new HttpRequestMessage(HttpMethod.Get, url);

        var response = await client.SendAsync(request);
        response.EnsureSuccessStatusCode();

        var vacancies = await response.Content.ReadFromJsonAsync<DouVacancyModel[]>();
        allVacanciesIds.AddRange(vacancies.Select(v => DouVacancyIdExtractor.GetId(v.Link)));
        return _mapper.Map<Vacancy[]>(vacancies.Where(v => isFirstRun || v.Date > DateTime.Today.AddDays(-1)));
    }
}