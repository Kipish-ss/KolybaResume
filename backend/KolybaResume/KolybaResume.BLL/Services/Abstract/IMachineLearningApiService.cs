using KolybaResume.BLL.Models;

namespace KolybaResume.BLL.Services.Abstract;

public interface IMachineLearningApiService
{
    Task<bool> NotifyResumeCreated(long resumeId);
    Task<VacancyScoreResponse[]> NotifyVacanciesUpdated(long[] vacancies);
    Task<VacancyScoreResponse[]> GetVacancyScores(long resumeId);
    Task<ResumeAdaptationResponse> GetResumeAdaptation(ResumeAdaptationRequest resumeAdaptationRequest);
}