using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using SeleniumExtras.WaitHelpers;

namespace KolybaResume.BLL.Services.Scrappers;

public static class DouCompanyScrapper
{
    public static string[] Scrape()
    {
        var options = new ChromeOptions();
        options.AddArgument("--headless");
        using var driver = new ChromeDriver(options);

        driver.Navigate().GoToUrl("https://jobs.dou.ua/companies/");

        var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));

        while (true)
        {
            try
            {
                var moreButton = wait.Until(ExpectedConditions.ElementToBeClickable(
                    By.LinkText("Більше компаній")
                ));
                
                var count = driver.FindElements(By.CssSelector("a.cn-a")).Count;

                if (count > 1500)
                {
                    break;
                }
                
                moreButton.Click();

                wait.Until(drv =>
                    drv.FindElements(By.CssSelector("a.cn-a")).Count > count
                );
            }
            catch (WebDriverTimeoutException)
            {
                break;
            }
            catch (NoSuchElementException)
            {
                break;
            }
        }

        return driver.FindElements(By.CssSelector("a.cn-a"))
            .Select(e => e.GetAttribute("href"))
            .Distinct()
            .ToArray()!;
    }
}