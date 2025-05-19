using System.Text.Json.Serialization;

namespace KolybaResume.BLL.Models;

public class ResumeAdaptationResponse
{
    public int ResumeId { get; set; }
    public int Score { get; set; }
    [JsonPropertyName("missing_keywords")]
    public string[] MissingKeywords { get; set; } = [];
}