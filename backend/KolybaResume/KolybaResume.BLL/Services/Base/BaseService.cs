using AutoMapper;
using KolybaResume.DAL.Context;

namespace KolybaResume.BLL.Services.Base;

public abstract class BaseService(KolybaResumeContext context, IMapper mapper)
{
    private protected readonly KolybaResumeContext _context = context;
    private protected readonly IMapper _mapper = mapper;
}