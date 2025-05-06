using KolybaResume.Common.DTO;

namespace KolybaResume.BLL.Services.Abstract;

public interface IUserService
{
    Task<UserDto> GetCurrent();
    Task<bool> CheckExisting(string email);
    Task<UserDto> Update(UserDto userDto, string currentUserEmail);
    Task<UserDto> Create(NewUserDto userDto);
    string? GetCurrentId();
    Task AddResume(string text);
    Task<long> GetResumeId();
}