FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src

COPY backend/KolybaResume/KolybaResume.csproj backend/KolybaResume/
RUN dotnet restore backend/KolybaResume/KolybaResume.csproj

COPY backend/KolybaResume/ backend/KolybaResume/
WORKDIR /src/backend/KolybaResume
RUN dotnet publish KolybaResume.csproj -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /app

COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://*:${PORT}

ENTRYPOINT ["dotnet", "KolybaResume.dll"]
