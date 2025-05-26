using KolybaResume.BLL.Services.Abstract;
using Microsoft.Extensions.Configuration;

namespace KolybaResume.BLL.Services;

using Mailjet.Client;
using Mailjet.Client.Resources;
using Newtonsoft.Json.Linq;

public class EmailService(IConfiguration configuration) : IEmailService
{
    private readonly MailjetClient _client = new(configuration["MailjetApiKey"], configuration["MailjetSecretKey"]);
    private const string FromEmail = "kolybaresume@gmail.com";
    private const string FromName = "Kolyba Resume";

    public async Task SendAsync(string toEmail, string toName, string subject, string text)
    {
        var request = new MailjetRequest
            {
                Resource = Send.Resource
            }
            .Property(Send.FromEmail, FromEmail)
            .Property(Send.FromName, FromName)
            .Property(Send.Subject, subject)
            .Property(Send.TextPart, text)
            .Property(Send.Recipients, new JArray
            {
                new JObject
                {
                    ["Email"] = toEmail,
                    ["Name"] = toName
                }
            });

        var response = await _client.PostAsync(request);
        if (!response.IsSuccessStatusCode)
        {
            throw new InvalidOperationException(
                $"Mailjet send failed: {response.StatusCode} {response.GetErrorMessage()}");
        }
    }
}