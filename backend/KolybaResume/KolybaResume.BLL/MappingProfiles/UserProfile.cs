using AutoMapper;
using KolybaResume.Common.DTO.User;
using KolybaResume.DAL.Entities;

namespace KolybaResume.BLL.MappingProfiles;

public class UserProfile : Profile
{
    public UserProfile()
    {
        CreateMap<User, UserDto>()
            .ForMember(user => user.HasResume, opt => opt.MapFrom(src => src.Resume != null));
        
        CreateMap<NewUserDto, User>();

        CreateMap<UserDto, User>();
    }
}