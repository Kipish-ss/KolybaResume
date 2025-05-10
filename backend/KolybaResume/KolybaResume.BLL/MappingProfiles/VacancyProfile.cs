using AutoMapper;
using KolybaResume.BLL.Services.Utility;
using KolybaResume.Common.DTO.Vacancy;
using KolybaResume.Common.Enums;
using KolybaResume.DAL.Entities;
using KolybaResume.DTO;
using Microsoft.IdentityModel.Tokens;

namespace KolybaResume.BLL.MappingProfiles;

public class VacancyProfile : Profile
{
    public VacancyProfile()
    {
        CreateMap<Vacancy, VacancyDto>();

        CreateMap<DouVacancyModel, Vacancy>()
            .ForMember(v => v.Text, opt => opt.MapFrom(m => m.Description))
            .ForMember(v => v.CategoryText, opt => opt.MapFrom(m => m.Category))
            .ForMember(v => v.Category, opt => opt.MapFrom(m => VacancyCategoryMapper.FromString(m.Category)))
            .ForMember(v => v.Url, opt => opt.MapFrom(m => m.Link));
    }
}