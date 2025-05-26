using KolybaResume.Common.DTO.User;

namespace KolybaResume.BLL.Services.Abstract;

public interface IUserService
{
    Task<UserDto> GetCurrent();
    Task<bool> CheckExisting(string email);
    Task<UserDto> Create(NewUserDto userDto);
    Task AddResume(string text);
    Task<long> GetResumeId();
}