using KolybaResume.BLL.Services.Abstract;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

namespace KolybaResume.BLL.Services.Scrappers;

public class DouVacancyScrapper : IVacancyScraper
{
    public async Task<string> Scrape(string url)
    {
        var options = new ChromeOptions();
        options.AddArgument("--headless");
        using var driver = new ChromeDriver(options);

        try
        {
            await driver.Navigate().GoToUrlAsync(url);

            var wait = new OpenQA.Selenium.Support.UI.WebDriverWait(driver, TimeSpan.FromSeconds(10));
            var vacancyDiv = wait.Until(d =>
                d.FindElement(By.CssSelector("div.l-vacancy"))
            );
            
            var titleElement = vacancyDiv.FindElement(By.CssSelector(".g-h2"));
            var descriptionElement  = vacancyDiv.FindElement(By.CssSelector(".b-typo.vacancy-section"));

            var title       = titleElement.Text.Trim();
            var description = descriptionElement.Text.Trim();

            return title + Environment.NewLine + description;
        }
        finally
        {
            driver.Quit();
        }
    }
}