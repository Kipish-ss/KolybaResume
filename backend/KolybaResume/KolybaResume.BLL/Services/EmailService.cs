using KolybaResume.BLL.Services.Abstract;
using Microsoft.Extensions.Configuration;

namespace KolybaResume.BLL.Services;

using Mailjet.Client;
using Mailjet.Client.Resources;
using Microsoft.Extensions.Options;
using Newtonsoft.Json.Linq;

public class EmailService(IConfiguration configuration) : IEmailService
{
    private readonly MailjetClient _client = new(configuration["MailjetApiKey"], configuration["MailjetSecretKey"]);
    private readonly string _fromEmail  = "kolybaresume@gmail.com";
    private readonly string _fromName   = "Kolyba Resume";

    public async Task SendAsync(string toEmail, string toName, string subject, string text)
    {
        var request = new MailjetRequest
        {
            Resource = Send.Resource,
        }
        .Property(Send.Messages, new JArray {
            new JObject {
                ["From"] = new JObject {
                    ["Email"] = _fromEmail,
                    ["Name"]  = _fromName
                },
                ["To"] = new JArray {
                    new JObject {
                        ["Email"] = toEmail,
                        ["Name"]  = toName
                    }
                },
                ["Subject"] = subject,
                ["TextPart"] = text
            }
        });

        var response = await _client.PostAsync(request);
        if (!response.IsSuccessStatusCode)
        {
            throw new InvalidOperationException($"Mailjet send failed: {response.StatusCode} {response.GetErrorMessage()}");
        }
    }

    private static string StripHtml(string html)
    {
        // simple fallback for plain-text part
        return System.Text.RegularExpressions
                     .Regex.Replace(html, "<.*?>", String.Empty);
    }
}