namespace KolybaResume.BLL.Services.Abstract;

public interface IVacancyScraperFactory
{
    IVacancyScraper GetScraper(string url);
}