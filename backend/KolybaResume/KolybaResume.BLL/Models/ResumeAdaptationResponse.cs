namespace KolybaResume.BLL.Models;

public class ResumeAdaptationResponse
{
    public int ResumesId { get; set; }
    public int Score { get; set; }
    public string[] MissingKeywords { get; set; } = [];
}