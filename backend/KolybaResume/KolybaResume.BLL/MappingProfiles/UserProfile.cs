using AutoMapper;
using KolybaResume.Common.DTO;
using KolybaResume.DAL.Entities;

namespace KolybaResume.BLL.MappingProfiles;

public class UserProfile : Profile
{
    public UserProfile()
    {
        CreateMap<User, UserDto>();
        
        CreateMap<NewUserDto, User>();

        CreateMap<UserDto, User>();
    }
}