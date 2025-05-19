using System.Net.Http.Json;
using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using Microsoft.Extensions.Configuration;

namespace KolybaResume.BLL.Services;

public class MachineLearningApiService : IMachineLearningApiService
{
    private readonly HttpClient _httpClient;
    private readonly string _apiUrl;

    public MachineLearningApiService(IConfiguration configuration, HttpClient httpClient)
    {
        httpClient.Timeout = TimeSpan.FromMinutes(15);
        _httpClient = httpClient;
        _apiUrl = configuration["MachineLearningBackendApi"]!;
    }

    public async Task<bool> NotifyResumeCreated(long resumeId)
    {
        var request = new
        {
            resume_id = resumeId
        };
        var response = await _httpClient.PutAsJsonAsync($"{_apiUrl}/resume", request);

        return response.IsSuccessStatusCode;
    }

    public async Task<VacancyScoreResponse[]> NotifyVacanciesUpdated(long[] vacancies)
    {
        var request = new
        {
            vacancy_ids = vacancies
        };
        var response = await _httpClient.PostAsJsonAsync($"{_apiUrl}/vacancies", request);

        return await response.Content.ReadFromJsonAsync<VacancyScoreResponse[]>();
    }

    public async Task<VacancyScoreResponse[]> GetVacancyScores(long resumeId)
    {
        var response = await _httpClient.GetAsync($"{_apiUrl}/vacancies/score/{resumeId}");

        return await response.Content.ReadFromJsonAsync<VacancyScoreResponse[]>();
    }

    public async Task<ResumeAdaptationResponse> GetResumeAdaptation(ResumeAdaptationRequest resumeAdaptationRequest)
    {
        var response = await _httpClient.PostAsJsonAsync($"{_apiUrl}/adaptation", resumeAdaptationRequest);

        return await response.Content.ReadFromJsonAsync<ResumeAdaptationResponse>();
    }
}