using AutoMapper;
using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.BLL.Services.Scrappers;
using KolybaResume.BLL.Services.Utility;
using KolybaResume.Common.DTO.Vacancy;
using KolybaResume.DAL.Context;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.BLL.Services;

public class VacancyService(
    KolybaResumeContext context,
    IMapper mapper,
    IMachineLearningApiService apiService,
    IUserService userService) : BaseService(context, mapper), IVacancyService
{
    public async Task<VacancyTextDto> ParseVacancy(string vacancyUrl)
    {
        if (vacancyUrl.Contains("jobs.dou.ua"))
        {
            var vacancy = await _context.Vacancies.FirstOrDefaultAsync(v => DouVacancyIdExtractor.Compare(v.Url, vacancyUrl));

            if (vacancy != null)
            {
                return new VacancyTextDto()
                {
                    Text = vacancy.Text,
                };
            }
        }

        if (vacancyUrl.Contains("www.postjobfree.com/job"))
        {
            return new VacancyTextDto()
            {
                Text = await (new PostJobFreeVacancyScrapper()).Scrape(vacancyUrl)
            };
        }

        throw new ArgumentException("Invalid URL");
    }

    public async Task<VacancyDto[]> Get()
    {
        var resumeId = await userService.GetResumeId();
        
        var scores = await apiService.GetVacancyScores(resumeId);
        
        var vacancies = await _context.Vacancies.Where(v => scores.Any(score => score.VacancyId == v.Id)).ToListAsync();
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