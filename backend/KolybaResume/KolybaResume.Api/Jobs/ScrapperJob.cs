using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Scrappers;

namespace KolybaResume.Jobs;

public class ScrapperJob(IServiceProvider services) : IHostedService
{
    public async Task StartAsync(CancellationToken cancellationToken)
    {
        try
        {
            using var scope = services.CreateScope();
            var companyService = scope.ServiceProvider.GetRequiredService<ICompanyService>();

            if (await companyService.HasCompanies())
            {
                return;
            }

            var companyLinks = DouCompanyScrapper.Scrape();
            await companyService.Create(companyLinks);
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}