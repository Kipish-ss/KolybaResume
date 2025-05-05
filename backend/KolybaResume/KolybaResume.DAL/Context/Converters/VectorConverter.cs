namespace KolybaResume.DAL.Context.Converters;

public static class VectorConverter
{
    public static byte[] ToBytes(double[] vector)
    {
        var bytes = new byte[vector.Length * sizeof(double)];
        Buffer.BlockCopy(vector, 0, bytes, 0, bytes.Length);
        return bytes;
    }

    public static double[] FromBytes(byte[] bytes)
    {
        var vector = new double[bytes.Length / sizeof(double)];
        Buffer.BlockCopy(bytes, 0, vector, 0, bytes.Length);
        return vector;
    }
}