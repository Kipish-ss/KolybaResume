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

            return vacancyDiv.Text.Trim();
        }
        finally
        {
            driver.Quit();
        }
    }
}