FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY KolybaResume.sln ./

COPY KolybaResume.Api/KolybaResume.Api.csproj KolybaResume.Api/
COPY KolybaResume.BLL/KolybaResume.BLL.csproj KolybaResume.BLL/
COPY KolybaResume.DAL/KolybaResume.DAL.csproj KolybaResume.DAL/
COPY KolybaResume.Common/KolybaResume.Common.csproj KolybaResume.Common/

RUN dotnet restore

COPY . .

WORKDIR /src/KolybaResume.Api
RUN dotnet publish -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=build /app/publish .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5050

ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:5050

ENTRYPOINT ["dotnet", "KolybaResume.Api.dll"]