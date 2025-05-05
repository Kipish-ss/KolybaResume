using System.Net.Http.Json;
using KolybaResume.BLL.Models;
using Microsoft.Extensions.Configuration;

namespace KolybaResume.BLL.Services;

public class MachineLearningApiService(IConfiguration configuration, HttpClient httpClient)
{
    private readonly string _apiUrl = configuration["MachineLearningBackendApi"]!;

    public async Task NotifyResumeCreated(long resumeId)
    {
        await httpClient.PostAsync($"{_apiUrl}/resumes/{resumeId}", null);
    }

    public async Task<VacancyScoreResponse[]> NotifyVacanciesUpdated(long[] vacancies)
    {
        var response = await httpClient.PostAsJsonAsync($"{_apiUrl}/vacancies", vacancies);
        
        return await response.Content.ReadFromJsonAsync<VacancyScoreResponse[]>();
    }

    public async Task<VacancyScoreResponse[]> GetVacancyScores(long[] vacancies)
    {
        var response = await httpClient.PostAsJsonAsync($"{_apiUrl}/vacancies/score", vacancies);
        
        return await response.Content.ReadFromJsonAsync<VacancyScoreResponse[]>();
    }

    public async Task<ResumeAdaptationResponse> GetResumeAdaptation(ResumeAdaptationRequest resumeAdaptationRequest)
    {
        var response = await httpClient.PostAsJsonAsync($"{_apiUrl}/adaptation", resumeAdaptationRequest);
        
        return await response.Content.ReadFromJsonAsync<ResumeAdaptationResponse>();
    }
}