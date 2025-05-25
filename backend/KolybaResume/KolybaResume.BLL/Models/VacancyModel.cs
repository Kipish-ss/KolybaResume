using KolybaResume.Common.Enums;

namespace KolybaResume.BLL.Models;

public class VacancyModel
{
    public string Title { get; set; }
    public string Link { get; set; }
    public string Location { get; set; }
    public string? Salary { get; set; }
    public string? Category { get; set; }
    public DateTime Date { get; set; }
    public string Description { get; set; }
    public VacancySource Source { get; set; }
}