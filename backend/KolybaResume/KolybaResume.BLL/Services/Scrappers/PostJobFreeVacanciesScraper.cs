using System.Globalization;
using KolybaResume.BLL.Models;
using KolybaResume.Common.Enums;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;

namespace KolybaResume.BLL.Services.Scrappers;

public static class PostJobFreeVacanciesScraper
{
    private const string BaseUrl = "https://www.postjobfree.com/jobs";

    public static List<VacancyModel> Scrape(string query)
    {
        var vacanciesList = new List<VacancyModel>();
        var options = new ChromeOptions();
        options.AddArgument("--headless");
        var driver = new ChromeDriver(options);
        var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
        
        try
        {
            var firstPageUrl = $"{BaseUrl}?q={Uri.EscapeDataString(query)}&r=100&p=1";
            driver.Navigate().GoToUrl(firstPageUrl);
            wait.Until(drv => drv.FindElements(By.CssSelector(".pager")).Any());

            var pagerLinksCount = driver
                .FindElements(By.CssSelector(".pager"))
                .Where(a =>
                {
                    var txt = a.Text.Trim();
                    return !string.Equals(txt, "Previous", StringComparison.OrdinalIgnoreCase)
                           && !string.Equals(txt, "Next", StringComparison.OrdinalIgnoreCase);
                })
                .Count();

            int totalPages = Math.Min(pagerLinksCount, 5);

            for (int page = 1; page <= totalPages; page++)
            {
                var listUrl = $"{BaseUrl}?q={Uri.EscapeDataString(query)}&r=100&p={page}";
                driver.Navigate().GoToUrl(listUrl);

                wait.Until(drv => drv.FindElements(By.CssSelector("h3 > a")).Count != 0);

                var jobLinks = driver
                    .FindElements(By.CssSelector("h3 > a"))
                    .Select(elem => elem.GetAttribute("href"))
                    .Where(link => link.Contains("postjobfree.com/job"))
                    .ToList();

                if (jobLinks.Count == 0)
                {
                    break;
                }

                foreach (var link in jobLinks)
                {
                    try
                    {
                        var vacancy = new VacancyModel
                        {
                            Link = link,
                            Source = VacancySource.PostJob,
                            Category = query
                        };

                        driver.Navigate().GoToUrl(link);
                        wait.Until(drv => drv.FindElement(By.TagName("h1")));

                        vacancy.Title = driver.FindElement(By.TagName("h1")).Text;
                        vacancy.Location = SafeFindText(By.CssSelector(".colorLocation"), driver);
                        vacancy.Salary = SafeFindText(By.CssSelector(".colorSalary"), driver);
                        vacancy.Date = DateTime.ParseExact(
                            SafeFindText(By.CssSelector(".colorDate"), driver),
                            "MMMM d, yyyy",
                            CultureInfo.InvariantCulture
                        );
                        vacancy.Description = driver.FindElement(By.CssSelector(".normalText")).Text.Trim();

                        vacanciesList.Add(vacancy);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine($"Unable to get vacancy, link: {link}");
                    }
                }
            }
        }
        finally
        {
            driver.Quit();
        }
        
        return vacanciesList;
    }

    private static string SafeFindText(By by, ChromeDriver driver)
    {
        try
        {
            return driver.FindElement(by).Text.Trim();
        }
        catch (NoSuchElementException)
        {
            return string.Empty;
        }
    }
}