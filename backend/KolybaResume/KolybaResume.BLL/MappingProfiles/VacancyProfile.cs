using AutoMapper;
using KolybaResume.Common.DTO.Vacancy;
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
            .ForMember(v => v.Url, opt => opt.MapFrom(m => m.Link));
    }
}