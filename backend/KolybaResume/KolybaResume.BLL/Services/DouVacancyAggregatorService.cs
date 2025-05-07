using System.Net;
using System.Net.Http.Json;
using AutoMapper;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;
using KolybaResume.DTO;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.BLL.Services;

public class DouVacancyAggregatorService(KolybaResumeContext context, IMapper mapper, HttpClient httpClient, IMachineLearningApiService apiService) : BaseService(context, mapper), IDouVacancyAggregatorService
{
    public async Task Aggregate()
    {
        var isFirstRun = !_context.Vacancies.Any();
        var companyLinks = await _context.Companies.Select(c => c.Url).ToListAsync();
        var addedVacanciesIds = new List<long>();

        foreach (var link in companyLinks)
        {
            var vacancies = await GetVacancies($"{link}vacancies/export/", isFirstRun);
            await _context.Vacancies.AddRangeAsync(vacancies);
            await _context.SaveChangesAsync();
            addedVacanciesIds.AddRange(vacancies.Select(v => v.Id));
        }
        
        
        //TODO: Uncomment when api is ready
        //await apiService.NotifyVacanciesUpdated(addedVacanciesIds.ToArray());
    }

    private async Task<Vacancy[]> GetVacancies(string url, bool isFirstRun)
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
        return _mapper.Map<Vacancy[]>(vacancies.Where(v => isFirstRun || v.Date > DateTime.Today.AddDays(-1)));
    }
}