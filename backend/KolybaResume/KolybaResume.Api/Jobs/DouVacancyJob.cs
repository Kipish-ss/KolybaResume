using KolybaResume.BLL.Services;
using Quartz;

namespace KolybaResume.Jobs;

public class DouVacancyJob(DouVacancyAggregatorService aggregatorService) : IJob
{
    public async Task Execute(IJobExecutionContext context)
    {
        await aggregatorService.Aggregate();
    }
}