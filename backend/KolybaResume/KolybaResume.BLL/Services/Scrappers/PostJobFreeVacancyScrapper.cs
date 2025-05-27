using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;

namespace KolybaResume.BLL.Services.Scrappers;

public class PostJobFreeVacancyScrapper
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
            var description = wait.Until(d => d.FindElement(By.CssSelector(".normalText")));

            return description.Text.Trim();
        }
        finally
        {
            driver.Quit();
        }
    }
}