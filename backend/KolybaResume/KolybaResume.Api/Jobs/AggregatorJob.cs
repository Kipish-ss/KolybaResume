using KolybaResume.BLL.Models;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;
using Microsoft.EntityFrameworkCore;
using Quartz;

namespace KolybaResume.Jobs;

public class AggregatorJob(IEnumerable<IAggregator> aggregators, KolybaResumeContext dbContext, IEmailService emailService, IMachineLearningApiService apiService) : IJob
{
    public async Task Execute(IJobExecutionContext context)
    {
        var addedVacancies = new List<Vacancy>();

        foreach (var aggregator in aggregators)
        {
            addedVacancies.AddRange(await aggregator.Aggregate());
        }
        
        var scores = new List<VacancyScoreResponse>();

        foreach (var batch in addedVacancies.Chunk(96))
        {
            scores.AddRange(await apiService.NotifyVacanciesUpdated(batch.Select(v => v.Id).ToArray()));
        }

        foreach (var userScore in scores.GroupBy(s => s.UserId))
        {
            var user = await dbContext.Users.FirstOrDefaultAsync(u => u.Id == userScore.Key);

            var relevantVacancies = userScore
                .Where(us => us.Score > 60)
                .Select(us => addedVacancies.First(v => v.Id == us.VacancyId)).ToArray();

            if (relevantVacancies.Length != 0 && user != null)
            {
                await emailService.SendAsync(
                    user.Email,
                    user.Name,
                    "New relevant vacancies",
                    string.Join(Environment.NewLine, relevantVacancies.Select(v => $"{v.Title}: {v.Url}")));
            }
        }
    }
}