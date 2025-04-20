using KolybaResume.BLL.Services;
using KolybaResume.Common.DTO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace KolybaResume.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class UserController(UserService userService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<UserDto>> GetCurrentUser()
    {
        var user = await userService.GetCurrent();
        return Ok(user);
    }

    [HttpPost]
    [AllowAnonymous]
    public async Task<ActionResult<UserDto>> CreateUserPreferences([FromBody] NewUserDto user)
    {
        return Ok(await userService.Create(user));
    }

    [HttpGet("check-email")]
    [AllowAnonymous]
    public async Task<ActionResult<bool>> CheckUserExistingByEmail(string email)
    {
        return Ok(await userService.CheckExisting(email));
    }

    [HttpPut]
    public async Task<IActionResult> UpdatePreferences([FromBody] UserDto user)
    {
        var currentUser = await userService.GetCurrent();

        var updatedUser = await userService.Update(user, currentUser.Email);

        return Ok(updatedUser);
    }
}