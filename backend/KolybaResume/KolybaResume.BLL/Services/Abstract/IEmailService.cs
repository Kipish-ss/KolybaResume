namespace KolybaResume.BLL.Services.Abstract;

public interface IEmailService
{
    Task SendAsync(string toEmail, string toName, string subject, string text);
}