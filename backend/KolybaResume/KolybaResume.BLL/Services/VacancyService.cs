using AutoMapper;
using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.Common.DTO.Vacancy;
using KolybaResume.DAL.Context;

namespace KolybaResume.BLL.Services;

public class VacancyService(KolybaResumeContext context, IMapper mapper, IMachineLearningApiService apiService, IUserService userService, IVacancyScraperFactory scraperFactory) : BaseService(context, mapper), IVacancyService
{
    public async Task<string> ParseVacancy(string vacancyUrl)
    {
        return await scraperFactory.GetScraper(vacancyUrl).Scrape(vacancyUrl);
    }

    public async Task<VacancyDto[]> Get()
    {
        var resumeId = await userService.GetResumeId();
        
        var scores = await apiService.GetVacancyScores(resumeId);
        
        var vacancies = _context.Vacancies.Where(v => scores.Any(score => score.VacancyId == v.Id));
        var dtos = _mapper.Map<VacancyDto[]>(vacancies);

        foreach (var dto in dtos)
        {
            dto.Score = scores.First(score => score.VacancyId == dto.Id).Score;
        }
        
        return dtos;
    }

    public async Task<ResumeAdaptationResponse> AdaptResume(string vacancyText)
    {
        var resumeId = await userService.GetResumeId();
        
        return await apiService.GetResumeAdaptation(new ResumeAdaptationRequest
        {
            ResumesId = resumeId,
            VacancyText = vacancyText
        });
    }
}