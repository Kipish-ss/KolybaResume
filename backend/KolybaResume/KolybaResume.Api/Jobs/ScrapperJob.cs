using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Scrappers;

namespace KolybaResume.Jobs;

public class ScrapperJob(IServiceProvider services) : IHostedService
{
    public async Task StartAsync(CancellationToken cancellationToken)
    {
        using var scope = services.CreateScope();
        var companyService = scope.ServiceProvider.GetRequiredService<ICompanyService>();
        var configuration = scope.ServiceProvider.GetRequiredService<IConfiguration>();

        if (!configuration.GetValue<bool>("ScrapeEnabled"))
        {
            return;
        }

        var companyLinks = DouCompanyScrapper.Scrape();
        await companyService.Create(companyLinks);
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}