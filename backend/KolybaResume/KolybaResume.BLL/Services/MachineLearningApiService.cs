using System.Net.Http.Json;
using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using Microsoft.Extensions.Configuration;

namespace KolybaResume.BLL.Services;

public class MachineLearningApiService(IConfiguration configuration, HttpClient httpClient) : IMachineLearningApiService
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

    public async Task<VacancyScoreResponse[]> GetVacancyScores(long resumeId)
    {
        var response = await httpClient.PostAsync($"{_apiUrl}/vacancies/score/{resumeId}", null);
        
        return await response.Content.ReadFromJsonAsync<VacancyScoreResponse[]>();
    }

    public async Task<ResumeAdaptationResponse> GetResumeAdaptation(ResumeAdaptationRequest resumeAdaptationRequest)
    {
        var response = await httpClient.PostAsJsonAsync($"{_apiUrl}/adaptation", resumeAdaptationRequest);
        
        return await response.Content.ReadFromJsonAsync<ResumeAdaptationResponse>();
    }
}