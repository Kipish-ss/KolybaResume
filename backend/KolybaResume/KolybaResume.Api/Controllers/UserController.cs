using KolybaResume.BLL.Services;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.Common.DTO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace KolybaResume.Controllers;

[Authorize]
[ApiController]
[Route("[controller]")]
public class UserController(IUserService userService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<UserDto>> GetCurrentUser()
    {
        var user = await userService.GetCurrent();
        return Ok(user);
    }

    [HttpPost]
    [AllowAnonymous]
    public async Task<ActionResult<UserDto>> Create([FromBody] NewUserDto user)
    {
        return Ok(await userService.Create(user));
    }

    [HttpGet("check-email")]
    [AllowAnonymous]
    public async Task<ActionResult<bool>> CheckUserExistingByEmail(string email)
    {
        return Ok(await userService.CheckExisting(email));
    }

    [HttpPost("resume")]
    [Consumes("multipart/form-data")]
    public async Task<IActionResult> ExtractText([FromForm] IFormFile file)
    {
        if (file == null || file.Length == 0)
        {
            return BadRequest("No file uploaded.");
        }

        string text;
        var ext = Path.GetExtension(file.FileName).ToLowerInvariant();

        using (var stream = file.OpenReadStream())
        {
            switch (ext)
            {
                case ".pdf":
                    text = TextExtractorService.ReadPdf(stream);
                    break;
                case ".docx":
                    text = TextExtractorService.ReadDocx(stream);
                    break;
                case ".doc":
                    text = TextExtractorService.ReadDoc(stream);
                    break;
                default:
                    return BadRequest("Unsupported file type.");
            }
        }
        
        await userService.AddResume(text);

        return Ok();
    }
}