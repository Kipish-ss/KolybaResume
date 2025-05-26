using KolybaResume.Common.Enums;

namespace KolybaResume.BLL.Models;

public class VacancyModel
{
    public string Title { get; set; } = string.Empty;
    public string Link { get; set; } = string.Empty;
    public string Location { get; set; } = string.Empty;
    public string? Salary { get; set; }
    public string? Category { get; set; }
    public DateTime Date { get; set; }
    public string Description { get; set; } = string.Empty;
    public VacancySource Source { get; set; }
}