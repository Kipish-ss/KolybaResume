using KolybaResume.BLL.Services.Abstract;

namespace KolybaResume.BLL.Services.Scrappers;

public class VacancyScraperFactory : IVacancyScraperFactory
{
    public IVacancyScraper GetScraper(string url)
    {
        if (url.Contains("jobs.dou.ua"))
        {
            return new DouVacancyScrapper();
        }

        if (url.Contains("www.postjobfree.com/job"))
        {
            return new PostJobFreeVacancyScrapper();
        }
        
        throw new ArgumentException("Invalid URL");
    }
}