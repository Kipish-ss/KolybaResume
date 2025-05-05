using AutoMapper;
using KolybaResume.Common.DTO.Vacancy;
using KolybaResume.DAL.Entities;

namespace KolybaResume.BLL.MappingProfiles;

public class VacancyProfile : Profile
{
    public VacancyProfile()
    {
        CreateMap<Vacancy, VacancyDto>();
    }
}