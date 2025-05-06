using KolybaResume.BLL.Services.Abstract;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;

namespace KolybaResume.BLL.Services.Scrappers;

public class PostJobFreeVacancyScrapper : IVacancyScraper
{
    public async Task<string> Scrape(string url)
    {
        var options = new ChromeOptions();
        options.AddArgument("--headless");
        using var driver = new ChromeDriver(options);

        try
        {
            await driver.Navigate().GoToUrlAsync(url);

            var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
            var descDiv = wait.Until(d =>
                d.FindElement(By.CssSelector("div[itemprop='description']"))
            );

            return descDiv.Text.Trim();
        }
        finally
        {
            driver.Quit();
        }
    }
}