using AutoMapper;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;

namespace KolybaResume.BLL.Services;

public class CompanyService(KolybaResumeContext context, IMapper mapper) : BaseService(context, mapper), ICompanyService
{
    public async Task Create(string[] links)
    {
        await _context.Companies.AddRangeAsync(links.Select(l => new Company { Url = l }));
        await _context.SaveChangesAsync();
    }
}