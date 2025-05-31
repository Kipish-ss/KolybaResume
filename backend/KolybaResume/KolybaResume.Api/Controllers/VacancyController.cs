using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.Common.DTO.Vacancy;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace KolybaResume.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class VacancyController(IVacancyService vacancyService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<VacancyDto[]>> Get()
    {
        var vacancies = await vacancyService.Get();
        return Ok(vacancies);
    }

    [HttpPost("recommendations")]
    public async Task<ActionResult<ResumeAdaptationResponse>> GetRecommendations([FromBody] AdaptationRequestDto vacancy)
    {
        var recommendations = await vacancyService.AdaptResume(vacancy.Description);
        return Ok(recommendations);
    }
    
    [HttpPost("recommendations/{vacancyId:long}")]
    public async Task<ActionResult<ResumeAdaptationResponse>> GetRecommendations(long vacancyId)
    {
        var recommendations = await vacancyService.AdaptResume(vacancyId);
        return Ok(recommendations);
    }

    [HttpPost("description")]
    public async Task<ActionResult<VacancyTextDto>> GetDescription([FromBody] VacancyDescriptionDto vacancy)
    {
        try
        {
            var description = await vacancyService.ParseVacancy(vacancy.Link);

            return Ok(description);
        }
        catch (Exception e)
        {
            return BadRequest(e.Message);
        }
    }
}