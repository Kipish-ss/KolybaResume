using KolybaResume.BLL.Services;
using KolybaResume.BLL.Services.Abstract;
using Quartz;

namespace KolybaResume.Jobs;

public class DouVacancyJob(IDouVacancyAggregatorService aggregatorService) : IJob
{
    public async Task Execute(IJobExecutionContext context)
    {
        await aggregatorService.Aggregate();
    }
}