using AutoMapper;
using KolybaResume.BLL.Services.Base;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;

namespace KolybaResume.BLL.Services;

public class CompanyService(KolybaResumeContext context, IMapper mapper) : BaseService(context, mapper)
{
    public void Create(string[] links)
    {
        _context.Companies.AddRange(links.Select(l => new Company { Url = l }));
        _context.SaveChanges();
    }
}