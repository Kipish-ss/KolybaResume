using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services;
using KolybaResume.Common.DTO.Vacancy;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace KolybaResume.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class VacancyController(VacancyService vacancyService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<VacancyDto[]>> Get()
    {
        var vacancies = await vacancyService.Get();
        return Ok(vacancies);
    }

    [HttpPost("recommendations")]
    public async Task<ActionResult<ResumeAdaptationResponse>> GetRecommendations([FromBody] string vacancy)
    {
        var recommendations = await vacancyService.AdaptResume(vacancy);
        return Ok(recommendations);
    }

    [HttpPost("description")]
    public async Task<ActionResult<string>> GetDescription([FromBody] string vacancyUrl)
    {
        var description = await vacancyService.ParseVacancy(vacancyUrl);
        
        return Ok(description);
    }
}