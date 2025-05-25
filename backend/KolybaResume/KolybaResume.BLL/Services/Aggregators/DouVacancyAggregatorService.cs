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
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.BLL.Services.Aggregators;

public class DouVacancyAggregatorService(KolybaResumeContext context, IMapper mapper) : BaseService(context, mapper), IAggregator
{
    public async Task<List<Vacancy>> Aggregate()
    {
        var isFirstRun = !_context.Vacancies.Any(v => v.Source == VacancySource.Dou);
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
        }
        
        return addedVacancies;
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

        var vacancies = await response.Content.ReadFromJsonAsync<VacancyModel[]>();
        allVacanciesIds.AddRange(vacancies.Select(v => DouVacancyIdExtractor.GetId(v.Link)));
        return _mapper.Map<Vacancy[]>(vacancies.Where(v => isFirstRun || v.Date > DateTime.Today.AddDays(-1)));
    }
}