using KolybaResume.BLL.Services.Abstract;
using Microsoft.Extensions.Configuration;

namespace KolybaResume.BLL.Services;

using Mailjet.Client;
using Mailjet.Client.Resources;
using Newtonsoft.Json.Linq;

public class EmailService(IConfiguration configuration) : IEmailService
{
    private readonly MailjetClient _client = new(configuration["MailjetApiKey"], configuration["MailjetSecretKey"]);
    private readonly string _fromEmail = "kolybaresume@gmail.com";
    private readonly string _fromName = "Kolyba Resume";

    public async Task SendAsync(string toEmail, string toName, string subject, string text)
    {
        var request = new MailjetRequest
            {
                Resource = Send.Resource
            }
            .Property(Send.FromEmail, _fromEmail)
            .Property(Send.FromName, _fromName)
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