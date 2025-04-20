namespace KolybaResume.Common.DTO;

public class UserDto
{
    public long Id { get; set; }
    public string Uid { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string? ImagePath { get; set; }
}