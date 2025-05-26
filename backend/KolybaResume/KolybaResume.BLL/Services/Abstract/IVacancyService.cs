using KolybaResume.Common.DTO.Vacancy;

namespace KolybaResume.BLL.Services.Abstract;

public interface IVacancyService
{
    Task<VacancyTextDto> ParseVacancy(string vacancyUrl);
    Task<VacancyDto[]> Get();
    Task<AdaptationResponseDto> AdaptResume(string vacancyText, bool shouldClean = true);
    Task<AdaptationResponseDto> AdaptResume(long vacancyId);
}