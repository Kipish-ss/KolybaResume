namespace KolybaResume.BLL.Services.Utility;

public static class DouVacancyIdExtractor
{
    public static int GetId(string url)
    {
        return url.Split("/").Where(s => int.TryParse(s, out _)).Select(int.Parse).Last();
    }

    public static bool Compare(string first, string second)
    {
        return GetId(first) == GetId(second);
    }
}