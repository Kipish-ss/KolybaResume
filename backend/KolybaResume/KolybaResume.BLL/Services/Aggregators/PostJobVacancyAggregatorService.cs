using AutoMapper;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.BLL.Services.Scrappers;
using KolybaResume.Common.Enums;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.BLL.Services.Aggregators;

public class PostJobVacancyAggregatorService(KolybaResumeContext context, IMapper mapper) : BaseService(context, mapper), IAggregator
{
    private static readonly string[] CategoryQueries = [
        "\"mobile developer\"",
        "\"customer support\"",
        "\"project manager\"",
        "devops",
        "\"data analyst\"",
        "qa",
        "\"sales manager\"",
        "\"ux designer\"",
    ];

    public async Task<List<Vacancy>> Aggregate()
    {
        var isFirstRun = !_context.Vacancies.Any(v => v.Source == VacancySource.PostJob);
        var addedVacancies = new List<Vacancy>();
        var allVacanciesLinks = new List<string>();

        try
        {
            foreach (var query in CategoryQueries)
            {
                var vacancies = PostJobFreeVacanciesScraper.Scrape(query);
                allVacanciesLinks.AddRange(vacancies.Select(v => v.Link));

                var vacanciesToAdd = _mapper.Map<Vacancy[]>(vacancies.Where(v => isFirstRun || v.Date > DateTime.Today.AddDays(-1)));
                await _context.Vacancies.AddRangeAsync(vacanciesToAdd);
                await _context.SaveChangesAsync();
                addedVacancies.AddRange(vacanciesToAdd);
            }
        }
        finally
        {
            var vacanciesToDelete = (await _context.Vacancies.ToListAsync())
                .Where(v => v.Source == VacancySource.PostJob &&
                            !allVacanciesLinks.Contains(v.Url));
            
            _context.Vacancies.RemoveRange(vacanciesToDelete);
            await _context.SaveChangesAsync();
        }
        
        return addedVacancies;
    }
}