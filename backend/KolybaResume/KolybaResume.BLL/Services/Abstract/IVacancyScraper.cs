namespace KolybaResume.BLL.Services.Abstract;

public interface IVacancyScraper
{
    Task<string> Scrape(string url);
}