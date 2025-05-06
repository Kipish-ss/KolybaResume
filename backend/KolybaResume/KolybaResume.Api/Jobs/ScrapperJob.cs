using KolybaResume.BLL.Services;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Scrappers;

namespace KolybaResume.Jobs;

public class ScrapperJob(IServiceProvider services) : IHostedService
{
    public Task StartAsync(CancellationToken cancellationToken)
    {
        using var scope = services.CreateScope();
        var companyService = scope.ServiceProvider.GetRequiredService<ICompanyService>();
        var configuration = scope.ServiceProvider.GetRequiredService<IConfiguration>();

        if (!configuration.GetValue<bool>("ScrapeEnabled"))
        {
            return Task.CompletedTask;
        }

        var companyLinks = DouCompanyScrapper.Scrape();
        companyService.Create(companyLinks);
        
        return Task.CompletedTask;
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}