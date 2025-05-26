using AutoMapper;
using FirebaseAdmin.Auth;
using KolybaResume.BLL.Extensions;
using KolybaResume.BLL.Services.Abstract;
using KolybaResume.BLL.Services.Base;
using KolybaResume.Common.DTO.User;
using KolybaResume.DAL.Context;
using KolybaResume.DAL.Entities;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;

namespace KolybaResume.BLL.Services;

public class UserService(KolybaResumeContext context, IMapper mapper, FirebaseAuth firebaseAuth, IHttpContextAccessor httpContextAccessor, IMachineLearningApiService apiService) : BaseService(context, mapper), IUserService
{
    public async Task<UserDto> GetCurrent()
    {
        var currentUser = await GetCurrentInternal();

        await AddClaims(currentUser.Uid, currentUser.Id);

        var currentUserDto = _mapper.Map<UserDto>(currentUser);
        return currentUserDto;
    }

    public async Task<bool> CheckExisting(string email)
    {
        return await _context.Users.AnyAsync(u => u.Email == email);
    }


    public async Task<UserDto> Create(NewUserDto userDto)
    {
        if (userDto is null)
        {
            throw new ArgumentNullException(nameof(userDto), "New user cannot be null");
        }

        var userEntity = await _context.Users.FirstOrDefaultAsync(u => u.Email.Equals(userDto.Email));
        if (userEntity is not null)
        {
            return _mapper.Map<UserDto>(userEntity);
        }

        var newUser = _mapper.Map<NewUserDto, User>(userDto);
        var user = (await _context.Users.AddAsync(newUser)).Entity;
        await _context.SaveChangesAsync();

        await AddClaims(user.Uid, user.Id);

        return _mapper.Map<User, UserDto>(user);
    }

    public async Task AddResume(string text)
    {
        var userId = (await GetCurrentInternal()).Id;
        var existingResume = await _context.Resumes.FirstOrDefaultAsync(r => r.UserId == userId);

        if (existingResume is not null)
        {
            _context.Resumes.Remove(existingResume);
        }
        var resume = new Resume
        {
            Text = text,
            UserId = userId
        };
        
        await _context.Resumes.AddAsync(resume);
        await _context.SaveChangesAsync();

        if (await apiService.NotifyResumeCreated(resume.Id))
        {
            return;
        }
        
        _context.Resumes.Remove(resume);
        await _context.SaveChangesAsync();
        
        throw new Exception("Could not add resume");
    }

    public async Task<long> GetResumeId()
    {
        var user = await GetCurrentInternal();
        return user.Resume?.Id ?? 0;
    }

    private async Task AddClaims(string? uid, long? id)
    {
        if (uid is null || id is null)
        {
            return;
        }

        var userRecord = await firebaseAuth.GetUserAsync(uid);

        if (userRecord.CustomClaims.ContainsKey("id"))
        {
            return;
        }

        var userClaims = new Dictionary<string, object>
        {
            { "id", id }
        };

        await firebaseAuth.SetCustomUserClaimsAsync(uid, userClaims);
    }

    private async Task<User> GetCurrentInternal()
        => await _context.Users.Include(u => u.Resume).FirstOrDefaultAsync(u => u.Uid == GetCurrentId())
            ?? throw new KeyNotFoundException("User doesn't exist");
    
    
    private string? GetCurrentId()
    {
        var userId = httpContextAccessor.HttpContext.User.GetUid();
        return userId;
    }
}