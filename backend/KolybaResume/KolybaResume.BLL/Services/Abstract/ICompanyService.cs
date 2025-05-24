namespace KolybaResume.BLL.Services.Abstract;

public interface ICompanyService
{
    Task Create(string[] links);
    Task<bool> HasCompanies();
}