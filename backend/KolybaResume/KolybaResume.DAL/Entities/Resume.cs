using KolybaResume.Common.Enums;

namespace KolybaResume.DAL.Entities;

public class Resume
{
    public long Id { get; set; }
    public long UserId { get; set; }
    public string Text { get; set; } = string.Empty;
    public string? CleanedText { get; set; }
    public double[]? Vector { get; set; }
    public string? Keywords { get; set; }
    public JobCategory? Category { get; set; }
    
    public User User { get; set; }
}